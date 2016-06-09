jest.unmock('../blog/static/blog/components');
import { ResultsItem } from '../blog/static/blog/components';

import TestUtils from 'react-addons-test-utils';
var React = require('react');
var ReactDOM = require('react-dom');

import chooseStory from '../blog/static/blog/discover3';


describe('ResultsItem', () => {
		it('should call changeFavStatus when heart icon is clicked', () => {
			
			var calledChangeFav = false;
			var toggle = () => {
				calledChangeFav = true;
			}
			
			const resultsItem = TestUtils.renderIntoDocument(< ResultsItem 
				key = {1}
				id = {1}
				title = ""
				link = ""
				hook = ""
				chooseStory = {chooseStory}
				isFav = {true}
				changeFavStatus = { toggle() }
			/>);
			
			TestUtils.Simulate.click(TestUtils.findRenderedDOMComponentWithTag(resultsItem, 'span'));

			expect(calledChangeFav).toBe(true);
			
		});
});