var React = require('react');
require('./discover');

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
				rows.push(<TagIconRow rowtags={rowTagList} key={i} searchByTag={this.props.searchByTag} tileIndexes={tileIndexes}/>);
				tileIndexes = [];
			}
		}
		
		return(
			<div className="row">
				<div className="col-lg-12 container">
					<div className="row">
						<label for="storytags_grid" className="col-lg-12">I want to...</label>
					</div>
					<div id="storytags_grid" className="row">
						<div className="col-lg-12 container">
							{rows}
						</div>
					</div>
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
			<div className={"tag_" + this.props.id + "_colour col-lg-3 tile"}>
				<div onClick={this.props.searchByTag} key ={this.props.key} id ={this.props.id} name ={this.props.name}>
					{this.props.name}
				</div>
			</div>
		)
    }
});