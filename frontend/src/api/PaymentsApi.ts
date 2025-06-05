import type { ClientSecret } from "@/types/Payment";
import type { TimeSlot } from "@/types/TimeSlot";
import axios from "axios";

const AxiosPaymentsApi = axios.create({
  baseURL: import.meta.env.VITE_PAYMENTS_API_URL,
  timeout: 10000,
});

class PaymentsApi {
  static async createCheckoutSession(timeslot: TimeSlot) {
    console.log("this triggered", timeslot);
    const { data } = await AxiosPaymentsApi.post<ClientSecret>("/checkout/", timeslot);
    console.log("payment:", data);
    return data;
  }
}

export { AxiosPaymentsApi, PaymentsApi };
