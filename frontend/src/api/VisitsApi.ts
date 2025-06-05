import type { DoctorTimeSlot, TimeSlot } from "@/types/TimeSlot";
import axios from "axios";

const AxiosVisitsApi = axios.create({
  baseURL: import.meta.env.VITE_VISITS_API_URL,
  timeout: 4800,
});


class VisitsApi {
  static async getTimeSlots() {
    const { data: timeslots } = await AxiosVisitsApi.get<TimeSlot[]>("/timeslots");
    return timeslots;
  }
}

export { AxiosVisitsApi, VisitsApi };

