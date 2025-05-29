export interface User {
    "id": string,
    "email": string,
    "first_name": string,
    "last_name": string,
    "role": UserRole,
};

export type UserRole = "lekarz" | "pacjent" | "guest";

export interface UserCreated {
    user: User,
    created: string,
    access_token: string,
    refresh: string
}