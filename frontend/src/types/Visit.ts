import type { Doctor } from "./Doctor";
import type { TimeSlot } from "./TimeSlot";

export interface Visit {
    id: string,
    doctor: Doctor,
    patient_id: string,
    time_slot: TimeSlot,
    status: "booked" | "cancelled" | "paid",
    notes: string
}