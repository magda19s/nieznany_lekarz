import { type FC } from "react";
import { EmbeddedCheckout, EmbeddedCheckoutProvider } from "@stripe/react-stripe-js";
import { loadStripe } from "@stripe/stripe-js";
import { useQuery } from "@tanstack/react-query";
import { PaymentsApi } from "@/api/PaymentsApi";
import { useAtom } from "jotai";
import { timeslotState } from "@/state/timeslot";
import { CircleAlert, Loader } from "lucide-react";
import type { TimeSlot } from "@/types/TimeSlot";
import { ScrollArea } from "@/components/ui/scroll-area";

const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_KEY);

const Payment: FC = () => {
    const [timeslot] = useAtom(timeslotState);
    
    const {
        data: secret,
        isError,
        isPending,
    } = useQuery({
        queryKey: ["client-secret", { timeslot }],
        queryFn: () =>
            PaymentsApi.createCheckoutSession(timeslot as TimeSlot),
        refetchOnWindowFocus: false,
    });

    return (
        <div className="flex h-full flex-col items-center justify-center relative -top-16">
            <h1 className="text-center text-xl font-bold md:text-3xl mb-4">Visit payment</h1>
            <div className="flex w-full flex-col items-center justify-center">
                {isPending ? (
                    <Loader className="animate-spin" />
                ) : isError ? (
                    <div className="mt-10 flex flex-col items-center justify-center gap-4">
                        <div className="flex gap-2 items-center">
                            <CircleAlert />
                            <span>Error loading payment data</span>
                        </div>
                    </div>
                ) : (
                    secret && (
                        <ScrollArea className="w-full max-h-[600px]">
                            <EmbeddedCheckoutProvider
                                stripe={stripePromise}
                                options={{ clientSecret: secret.client_secret }}
                            >
                                <EmbeddedCheckout />
                            </EmbeddedCheckoutProvider>
                        </ScrollArea>
                    )
                )}
            </div>
        </div>
    );
};

export default Payment;
