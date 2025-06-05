export interface ClientSecret {
  client_secret: string;
}

export interface PaymentStatus {
  status: string;
  payment_status: Status;
  customer_email: string;
}

export type Status = "paid" | "unpaid";
