import axios from 'axios';

const baseURL =  '/';

const instance = axios.create({ baseURL, validateStatus: () => true });

instance.interceptors.request.use(
	(request) => {
		return request;
	},
	(error) => {
		return Promise.reject(error);
	},
);

export const Axios = () => instance;
