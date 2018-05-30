import axios from 'axios'

const endpoint = 'http://localhost:5000/'

const ServerAPI = {
  async getMessageBody () {
    const res = await axios.get(endpoint)
    console.log(res.data)
    return res.data
  }
}

export default ServerAPI
