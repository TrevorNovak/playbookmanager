
import React, { Component } from 'react';
import { connect } from 'react-redux';
import './PlaybooksScreen.css';

class PlaybooksScreen extends Component {
  render() {
    return (
      <h2>List of Playbooks:</h2>
    );
  }
}

function mapStateToProps(state) {
  return {};
}

export default connect(mapStateToProps)(PlaybooksScreen);
