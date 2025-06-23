export interface ClientSecret {
  client_secret: string;
}

export type Status = "paid" | "unpaid";

export interface PaymentStatus {
  metadata: {
    user_id: string,
    visit_id: string,
    doctor_id: string
  },
  status: "paid" | "unpaid"
};
