var React = require('react');
var Sidebar = require('./sidebar')
var Featurespace = require('./featurespace')

export var App = React.createClass({

                getInitialState: function() {
                    var tagList = [];
                    return{
                        featureSpaceStoryId: 0,
						selectedStory: {},
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
							url: '/rest-api/stories/',
							data: {
								tagId: 0,
								titleText: ""
							},
							type: 'GET',
							dataType: 'json'
					})
					.done( (response) => {
							this.setState({startingStoryList: response, currentStoryList: response});
							console.log(this.state.startingStoryList);
					})
					.fail( (xhr, status, err) => {
							console.error(status, String(err));
					});
					
                    this.getTagList();
                },
                getTagList: function() {
                    $.ajax({
						url: '/rest-api/tags/',
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
					var filteredList = [];
					var url = '/rest-api/stories/'
					if (tag_id > 0 || title_text) {
						url = url + '?';
					}
					if(tag_id > 0) {
						url = url + 'tag_id=' + tag_id;
					}
					if (tag_id > 0 && title_text) {
						url = url + '&';
					}
					if(title_text) {
						url = url + 'title_text=' + title_text;
					}
					if (tag_id > 0 || title_text) {
						$.ajax({
							url: url,
							data: {
								tagId: tag_id,
								titleText: title_text
							},
							type: 'GET',
							dataType: 'json'
						})
						.done( (response) => {
							filteredList = response;
							this.setState({currentStoryList: filteredList});
						})
						.fail( (xhr, status, err) => {
							console.error(status, String(err));
						});
					}
					else {
						filteredList = this.state.startingStoryList;
						this.setState({currentStoryList: filteredList});
					}
                },
                searchByTag(event){
                    var tag_id = event.target.id;
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
                    this.setState({featureSpaceStoryId: event.target.id});
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
					
					for (var index in this.state.currentStoryList){
                        if (this.state.currentStoryList[index].id == this.state.featureSpaceStoryId) {
							this.state.selectedStory = this.state.currentStoryList[index];
                        }
                    };
					
                    return(
                        <div className="row">
                            <Sidebar.Sidebar
                                currentStoryList = {this.state.currentStoryList}
                                searchByTitle = {this.searchByTitle}
                                searchByTag = {this.searchByTag}
                                tagList = {this.state.tagList}
                                placeholderText = {this.state.placeholderText}
                                chooseStory = {this.chooseStory}
                                changeFavStatus = {this.changeFavStatus}
								tagInput = {this.state.tagInput}
                            />
                            <Featurespace.Featurespace
								story={this.state.selectedStory}
                                changeFavStatus = {this.changeFavStatus}
                            />
                        </div>
                    )
                }
});

