import type { ClientSecret, PaymentStatus } from "@/types/Payment";
import type { Visit } from "@/types/Visit";
import axios from "axios";

const AxiosPaymentsApi = axios.create({
  baseURL: import.meta.env.VITE_PAYMENTS_API_URL,
  timeout: 10000,
});

class PaymentsApi {
  static async createCheckoutSession(visit: Visit) {
    const { data } = await AxiosPaymentsApi.post<ClientSecret>("/checkout/", visit);
    return data;
  }
  
  static async getSessionStatus(session_id: string) {
    const { data } = await AxiosPaymentsApi.get<PaymentStatus>(
      `/payment/status/${session_id}/`,
    );
    return data;
  }
}

export { AxiosPaymentsApi, PaymentsApi };
