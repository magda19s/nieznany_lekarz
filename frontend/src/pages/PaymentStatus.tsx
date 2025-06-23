import { PaymentsApi } from '@/api/PaymentsApi';
import { cn } from '@/lib/utils';
import { useQuery } from '@tanstack/react-query';
import { CheckCircle, CircleAlert, Loader, XCircle } from 'lucide-react';
import { type FC } from 'react'
import { useSearchParams } from 'react-router-dom';

const PaymentStatus: FC = () => {
    const [searchParams] = useSearchParams();
    const session_id = searchParams.get('session_id') ?? '';

    const { data: status, isError, isPending } = useQuery({
        queryKey: ["payment-status"],
        queryFn: () => PaymentsApi.getSessionStatus(session_id),
        enabled: Boolean(session_id)
    })

    if (isPending) {
        return <Loader className='animate-spin mx-auto mt-10' />
    }
    if (isError || !status) {
        return (<div className="mt-10 flex flex-col items-center justify-center gap-4">
            <div className="flex gap-2 items-center">
                <CircleAlert />
                <span>Error loading payment status data</span>
            </div>
        </div>)
    }
    const isUnpaid = status.status === "unpaid"

    return (
        <div className='flex h-full flex-col items-center justify-center relative -top-16 gap-3'>{
            isUnpaid ? (
                <XCircle size={50} className="mb-6 text-destructive" />
            ) : (
                <CheckCircle size={50} className="mb-6" />
            )}
            <h3 className={cn("text-center text-3xl font-bold", isUnpaid ? "text-red-600" : "text-green-700")}>
                {isUnpaid ? "Payment  failed" : "Payment completed successfully"}
            </h3>
            <p className="text-justify opacity-70 max-w-[600px] text-lg">
                {isUnpaid ? "Your payment for the appointment was not completed. Please try again or contact us for assistance." : "Your payment for the appointment has been successfully processed. Thank you for using our clinic's services. If you have any questions or concerns, please feel free to contact us."
                }
            </p></div>
    )
}

export default PaymentStatus;
