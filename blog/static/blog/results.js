var React = require('react');
require('./discover');

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