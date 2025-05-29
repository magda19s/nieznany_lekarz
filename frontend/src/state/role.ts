
import type { UserRole } from "@/types/User";
import { atom } from "jotai";

export const roleState = atom<UserRole>("guest");
