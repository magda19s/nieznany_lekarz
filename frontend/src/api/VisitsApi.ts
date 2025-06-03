import axios from "axios";

const AxiosVisitsApi = axios.create({
  baseURL: import.meta.env.VITE_VISITS_API_URL,
  timeout: 4800,
});

export { AxiosVisitsApi };
