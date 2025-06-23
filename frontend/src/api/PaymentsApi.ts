import type { ClientSecret } from "@/types/Payment";
import type { TimeSlot } from "@/types/TimeSlot";
import axios from "axios";

const AxiosPaymentsApi = axios.create({
  baseURL: import.meta.env.VITE_PAYMENTS_API_URL,
  timeout: 10000,
});

class PaymentsApi {
  static async createCheckoutSession(timeslot: TimeSlot) {
    const { data } = await AxiosPaymentsApi.post<ClientSecret>("/checkout/", timeslot);
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
