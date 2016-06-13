//import React from 'react';

var React = require('react');
require('./discover3');

export var Sidebar = React.createClass({
    render: function() {
        return(
            <div id="side_bar" className="col-xs-4">
                <div className="row" id="search_tools">
                    <form className="form-horizontal col-xs-12">
                        <Tagsearch searchByTag={this.props.searchByTag} tagList ={this.props.tagList}/>
						<Titlesearch searchByTitle={this.props.searchByTitle} placeholderText={this.props.placeholderText}/>
                    </form>
                </div>
                <div className="row" id="list_of_stories">
                    <div className="col-xs-12">
                        <Results
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

export var Tagsearch = React.createClass({
    render: function() {

        var tagsObj = this.props.tagList;
		var tagList = [];
		for (var obj in tagsObj) {
			tagList.push({id: tagsObj[obj].id, name: tagsObj[obj].name});
		}
		tagList.splice(0, 0, {id: 0, name: "see all stories"});
		var rows = [];
		var counter=0;
		var tileIndexes = [];
		for (var i in tagList) {
			if(parseInt(i)%3 === 0) {
				var rowTagList = [];
				var x = 0, y = 3;
				if (tagList.length < (parseInt(i)+3) ) {
					y = tagList.length - parseInt(i);
				}
				for (x = 0; x<y; x++) {
					var index = x + parseInt(i);
					rowTagList.push(tagList[index]);
					tileIndexes.push(counter);
					counter++;
				}
				rows.push(<TagIconRow rowtags={rowTagList} key={i} searchByTag={this.props.searchByTag} tileIndexes={tileIndexes} />);
				tileIndexes = [];
			}
		}
		
		return(
			<div>
				<label for="storytags_grid">I want to...</label>
				<div id="storytags_grid">
					{rows}
				</div>
			</div>
		);
    }
});

export var TagIconRow = React.createClass({
	render: function() {
		var tagList = this.props.rowtags;
		var tags = [];
		for (var i in tagList) {
			var counter = this.props.tileIndexes[i];
			tags.push(<Option key={tagList[i].id} id={tagList[i].id} name={tagList[i].name} searchByTag={this.props.searchByTag} counter={counter}/>);
		}
		return(
			<div className="row">
				{tags}
			</div>
		);
	}
});

export var Option = React.createClass({
    render: function() {
		return(
			<div id={"tag_icon_" + this.props.counter} className="col-lg-3">
				<div onClick={this.props.searchByTag} key ={this.props.key} id ={this.props.id} name ={this.props.name}>
					{this.props.name}
				</div>
			</div>
		)
    }
});

export var Titlesearch = React.createClass({
    render: function() {
        return(
            <div className="row">
                <div className="form-group form-group-lg col-xs-12">
                    <label for="searchterm" className="control-label col-xs-4">Search by title:</label>
                    <div className="col-xs-8">
                        <input id="searchterm" type="text" placeholder={this.props.placeholderText}
                        onChange={this.props.searchByTitle} className="form-control" />
                    </div>
                </div>
            </div>
        )
    }
});

export var Results = React.createClass({
    render: function() {
        var items = [];
        for(var story in this.props.currentStoryList) {
            var pagelink = '/blog/' + String(this.props.currentStoryList[story].id) + '/';
            items.push(<ResultsItem
                key={this.props.currentStoryList[story].id}
                id={this.props.currentStoryList[story].id}
                title={this.props.currentStoryList[story].title}
                link={pagelink}
                hook={this.props.currentStoryList[story].hook}
                chooseStory={this.props.chooseStory}
                isFav={this.props.currentStoryList[story].is_fav}
                changeFavStatus={this.props.changeFavStatus}
            />);
        }
        if (items.length == 0) {
                return(<p>No stories found</p>);
        }
        else {
            return(
                <ul className="list-unstyled">
                    {items}
                    <div id="pagelimit" className="text-right small">
                        <p>Showing X results of Y</p>
                        <p>Show more</p>
                    </div>
                </ul>
            );
        };
    }
});

export var ResultsItem = React.createClass({
    render: function() {
       return(
            <li className="bg-success">
                <h4 id={this.props.id} onClick={this.props.chooseStory}>
                    {this.props.title}
                </h4>
                    <span
                        className={this.props.isFav ? "glyphicon glyphicon-heart" : "glyphicon glyphicon-heart-empty"}
                        aria-hidden="true"
                        id={this.props.id}
                        onClick={this.props.changeFavStatus}>
                    </span>
                <p>{this.props.hook}</p>
            </li>
        )
    }
});


export var Featurespace = React.createClass({
    render: function() {
        var story_text_paras = []
        for (var para in this.props.story.storytext) {
            story_text_paras.push(< Para key={para} id={para} text={this.props.story.storytext[para]} />);
        }
        return(
            <div id="featureSpace" className="col-xs-8">
                <h2>
                    {this.props.story.title}
                    <span>    </span>
                    <span
                        id={this.props.story.id}
                        className={this.props.story.is_fav ? "glyphicon glyphicon-heart" : "glyphicon glyphicon-heart-empty"}
                        aria-hidden="true"
                        onClick={this.props.changeFavStatus}
                        >
                    </span>
                </h2>
                <div id="buttons" className="row">
                    <div className="col-xs-5"></div>
                    <button className="btn btn-primary btn-sm col-xs-2">
                        <span className="glyphicon glyphicon-book" aria-hidden="true"></span>  Download PDF
                    </button>
                    <button className="btn btn-primary btn-sm col-xs-2">
                        <span className="glyphicon glyphicon-headphones" aria-hidden="true"></span>  Download MP3
                    </button>
                    <button className="btn btn-primary btn-sm col-xs-2">
                        <span className="glyphicon glyphicon-play" aria-hidden="true"></span>  Play
                    </button>
                </div>
                <div>{story_text_paras}</div>
            </div>
        )
    }
});

export var Para = React.createClass({
    render: function() {
        return(
            <p className={this.props.id == 0 ? "lead" : null}>{this.props.text}</p>
        )
    }
});