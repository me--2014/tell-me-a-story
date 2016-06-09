var React = require('react');
var components = require('./components');

export var App = React.createClass({

                getInitialState: function() {
                    var tagList = [];
                    return{
                        featureSpaceStory: {},
                        tagList: tagList,
                        placeholderText: "Start typing to search",
                        startingStoryList: [],
                        currentStoryList: [],
                        tagInput: 0,
                        textInput: ""
                    }
                },
                componentWillMount: function() {
                    $.ajax({
                        url: '/blog/0/getTaggedStories/',
                        dataType: 'json',
                        success: function(data) {
                            this.setState({startingStoryList: data, currentStoryList: data, featureSpaceStory: data['0']});
                        }.bind(this),
                        error: function(xhr, status, err) {
                            console.error(status, String(err));
                        }.bind(this)
                    });
                    this.getTagList();
                },
                getTagList: function() {
                    $.ajax({
                        url: '/blog/getTags/',
                        dataType: 'json',
                        success: function(data) {
                            this.setState({tagList: data});
                        }.bind(this),
                        error: function(xhr, status, err) {
                            console.error(status, String(err));
                        }.bind(this)
                    });
                },
                filter: function(tag_id, title_text) {
                    var startingList = this.state.startingStoryList;
                    var filteredByTagList = startingList;
                    var filteredByTitleList = [];
                    $.ajax({
                        url: '/blog/' + tag_id + '/getTaggedStories/',
                        dataType: 'json',
                        success: function(data) {
                            //Filter by tag
                            if(tag_id > 0){
                                filteredByTagList = data;
                            }
                            //Filter by title text
                            if (title_text) {
                                var searchTerm = title_text.toLowerCase();
                                for (var story in filteredByTagList) {
                                    var title = filteredByTagList[story].title.toLowerCase();
                                    if(title.indexOf(searchTerm) != -1) {
                                        filteredByTitleList.push({
                                            id: filteredByTagList[story].id,
                                            title: filteredByTagList[story].title,
                                            hook: filteredByTagList[story].hook
                                        });
                                    }
                                }
                            }
                            else {
                                filteredByTitleList = filteredByTagList;
                            }
                            this.setState({currentStoryList: filteredByTitleList});
                        }.bind(this),
                        error: function(xhr, status, err) {
                            console.error(status, String(err));
                        }.bind(this)
                    });
                },
                searchByTag(event){
                    var tag_id = event.target.value;
                    var title_text = this.state.textInput;
                    this.filter(tag_id, title_text);
                    this.setState({tagInput: tag_id});
                },
                searchByTitle(event){
                    var tag_id = this.state.tagInput;
                    var title_text = event.target.value;
                    this.filter(tag_id, title_text);
                    this.setState({textInput: title_text});
                },
                chooseStory(event) {
                    var chosenStoryId = event.target.id;
                    for (var index in this.state.startingStoryList){
                        if (this.state.startingStoryList[index].id == chosenStoryId) {
                            this.setState({featureSpaceStory: this.state.startingStoryList[index]});
                        }
                    };
                },
                changeFavStatus(event) {

                    var storyId = event.target.id;
                    var currentStoryList = this.state.currentStoryList;
                    for (var story in currentStoryList) {
                        if(currentStoryList[story].id === parseInt(storyId)) {
                            var selectedStory = currentStoryList[story];
                        }
                    }

                    if(selectedStory.is_fav === false) {
                        selectedStory.is_fav = true;
                    }
                    else{
                        selectedStory.is_fav = false;
                    }

                    this.setState({currentStoryList: currentStoryList});

                    /*
                    //Update server
                    var request = $.ajax({
                        method: 'POST',
                        url: '/blog/toggleFav/',
                        data: {userId: 1, story_id: storyId},
                        });
                    request.done(function(msg) {
                        //Do nothing
                    });
                    request.fail(function(jqXHR, textStatus) {
                        alert("Failed to save preference permanently:" + textStatus);
                    });
                    */

                },
                render: function() {
                    return(
                        <div className="row">
                            <components.Sidebar
                                currentStoryList = {this.state.currentStoryList}
                                searchByTitle = {this.searchByTitle}
                                searchByTag = {this.searchByTag}
                                tagList = {this.state.tagList}
                                placeholderText = {this.state.placeholderText}
                                chooseStory = {this.chooseStory}
                                changeFavStatus = {this.changeFavStatus}
                            />
                            <components.Featurespace
                                story={this.state.featureSpaceStory}
                                changeFavStatus = {this.changeFavStatus}
                            />
                        </div>
                    )
                }
});

