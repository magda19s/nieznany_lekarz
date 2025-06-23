import type { TimeSlot } from "@/types/TimeSlot";
import type { Visit } from "@/types/Visit";
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

  static async createVisit(timeslot_id: string) {
    const { data: visit } = await AxiosVisitsApi.post<Visit>(`/visits/${timeslot_id}`);
    return visit;
  }
}

export { AxiosVisitsApi, VisitsApi };

