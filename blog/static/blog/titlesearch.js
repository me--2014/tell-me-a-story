var React = require('react');
require('./discover');


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