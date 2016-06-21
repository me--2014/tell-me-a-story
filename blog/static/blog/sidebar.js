var React = require('react');
require('./discover');
var Tagsearch = require('./tagsearch')
var Titlesearch = require('./titlesearch')
var Results = require('./results')

export var Sidebar = React.createClass({
    render: function() {
		var tagId = this.props.tagInput;
		var results_list_class = "tag_" + tagId + "_colour"
		
        return(
            <div id="side_bar" className="col-xs-4 container">
                <div className="row" id="search_tools">
                    <form className="form-horizontal col-xs-12 container">
                        <Tagsearch.Tagsearch searchByTag={this.props.searchByTag} tagList ={this.props.tagList}/>
						<Titlesearch.Titlesearch searchByTitle={this.props.searchByTitle} placeholderText={this.props.placeholderText}/>
                    </form>
                </div>
                <div className="row" id="list_of_stories">
                    <div className={"col-xs-12 " + results_list_class}>
                        <Results.Results
                            currentStoryList={this.props.currentStoryList}
                            chooseStory={this.props.chooseStory}
                            changeFavStatus={this.props.changeFavStatus}
                        />
                    </div>
                </div>
            </div>
        )
    }
});