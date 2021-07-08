
import React from 'react';
import APIClient from '../apiClient'

class Home extends React.Component {
    state = {
        count: 0,
    };
  
    componentDidMount() {
      this.apiClient = new APIClient();
      this.apiClient.getCount().then((data) =>
        this.setState({...this.state, count: data})
      );
    }
    render() {
        return (
          <div>
            {this.state.count}
          </div>
        );
      }
}
export default Home;