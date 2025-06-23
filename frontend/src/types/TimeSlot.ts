import type { Doctor } from "./Doctor";

export interface TimeSlot {
    id: string,
    start: string,
    end: string,
    is_available: string,
    doctor: Doctor
}