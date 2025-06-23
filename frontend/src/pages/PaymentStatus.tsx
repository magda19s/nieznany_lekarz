import { PaymentsApi } from '@/api/PaymentsApi';
import { useQuery } from '@tanstack/react-query';
import { type FC } from 'react'
import { useSearchParams } from 'react-router-dom';

const PaymentStatus: FC = () => {
    const [searchParams] = useSearchParams();
    const session_id = searchParams.get('session_id') ?? '';

    const { data: status } = useQuery({
        queryKey: ["payment-status"],
        queryFn: () => PaymentsApi.getSessionStatus(session_id),
        enabled: Boolean(session_id)
    })

    console.log(status);

    return (
        <div>PaymentStatus</div>
    )
}

export default PaymentStatus;
