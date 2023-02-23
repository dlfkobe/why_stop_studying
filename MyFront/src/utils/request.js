import axios from "axios"

const request = new axios.create({
    baseURL: '/du',
    timeout: 5000,
})

export default request