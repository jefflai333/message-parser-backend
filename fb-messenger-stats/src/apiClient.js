import axios from 'axios';

const BASE_URI = 'http://localhost:3000';

const client = axios.create({
 baseURL: BASE_URI,
 json: true
});

class APIClient {
  constructor(accessToken) {
    this.accessToken = accessToken;
  }

//   createKudo(repo) {
//     return this.perform('post', '/kudos', repo);
//   }

//   deleteKudo(repo) {
//     return this.perform('delete', `/kudos/${repo.id}`);
//   }

  getCount() {
    return this.perform('get', '/table');
  }

  async perform (method, resource, data) {
    return client({
      method,
      url: resource,
      data,
    }).then(resp => {
      return resp.data ? resp.data : [];
    })
  }
}

export default APIClient;