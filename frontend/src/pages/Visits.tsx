import { roleState } from '@/state/role'
import { useAtom } from 'jotai'
import { type FC } from 'react'
import DoctorVisits from './DoctorVisits';
import PatientVisits from './PatientVisits';

const Visits: FC = () => {
    const [role] = useAtom(roleState);

    if (role === "doctor") return <DoctorVisits />;
    if (role === "patient") return <PatientVisits />;
    return <></>
}

export default Visits