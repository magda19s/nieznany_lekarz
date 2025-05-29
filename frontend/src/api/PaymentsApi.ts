import axios from "axios";

const AxiosPaymentsApi = axios.create({
  baseURL: import.meta.env.VITE_PAYMENTS_API_URL,
  timeout: 4800,
});

export {AxiosPaymentsApi};
