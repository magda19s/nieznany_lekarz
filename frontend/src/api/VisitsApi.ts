import type { TimeSlot } from "@/types/TimeSlot";
import type { User } from "@/types/User";
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

  static async getDoctorVisits() {
    const { data: visits } = await AxiosVisitsApi.get<Visit[]>("visits/doctor/");
    return visits;
  }

  static async getPatientVisits() {
    const { data: visits } = await AxiosVisitsApi.get<Visit[]>("visits/patient/");
    return visits;
  }

  static async addVisitNote(visit_id: string, notes: string) {
    const { data: visit } = await AxiosVisitsApi.patch<Visit>(`/visits/${visit_id}/doctor/`, { notes });
    return visit;
  }

  static async getPatient(patient_id: string) {
    const { data: patient } = await AxiosVisitsApi.get<User>(`/patient/${patient_id}/`);
    return patient;
  }
}

export { AxiosVisitsApi, VisitsApi };

