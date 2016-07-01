var React = require('react');
require('./discover');

export var Featurespace = React.createClass({
    render: function() {
		
		var story_for_render = []
		var fulltext = this.props.story.storytext;
		if(fulltext) {
			var text_with_paras = fulltext.split('\n');
			for (var para in text_with_paras) {
				story_for_render.push(< Para key={para} id={para} text={text_with_paras[para]} />);
			}
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
                <div>{story_for_render}</div>
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