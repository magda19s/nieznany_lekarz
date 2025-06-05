import { VisitsApi } from '@/api/VisitsApi';
import Avatar from '@/components/Avatar';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { cn } from '@/lib/utils';
import { roleState } from '@/state/role';
import type { Doctor } from '@/types/Doctor';
import type { TimeSlot } from '@/types/TimeSlot';
import { stringToColor } from '@/utils/avatar';
import { formatWeekDayName, formatTime, formatDate } from '@/utils/formatter';
import { useQuery } from '@tanstack/react-query';
import { useAtom } from 'jotai';
import { Calendar, CircleAlert, Loader } from 'lucide-react';
import { useMemo, useState, type FC } from 'react'

const BookAService: FC = () => {
    const [role] = useAtom(roleState);
    const { data: timeslots, isPending, isError } = useQuery({
        queryKey: ["timeslots"],
        queryFn: VisitsApi.getTimeSlots,
        enabled: ["patient", "pacjent"].includes(role)
    });

    const [timeslot, setTimeslot] = useState<TimeSlot | null>(null);
    const [doctor, setDoctor] = useState<Doctor | null>(null);

    const filteredTimeSlots = useMemo(() => {
        if (!timeslots) return [];

        let filtered = timeslots
            .filter(slot => slot.is_available);

        if (doctor) {
            filtered = timeslots
                .filter(slot => slot.doctor.doctor_id === doctor.doctor_id)

        }
        return filtered;

    }, [doctor, timeslots]);

    const availableDoctors = useMemo(() => {
        if (!timeslots) return [];

        const seen = new Set();
        const uniqueDoctors = [];

        for (const slot of timeslots) {
            const doc = slot.doctor;
            if (!seen.has(doc.doctor_id)) {
                seen.add(doc.doctor_id);
                uniqueDoctors.push(doc);
            }
        }

        return uniqueDoctors;
    }, [timeslots]);

    const groupedTimeSlots = useMemo(() => {
        if (!filteredTimeSlots) return {};

        return filteredTimeSlots.reduce((acc, slot) => {
            const date = new Date(slot.start);
            const dayKey = formatDate(date); // np. "05.06.2025"

            if (!acc[dayKey]) {
                acc[dayKey] = [];
            }
            acc[dayKey].push(slot);
            return acc;
        }, {} as Record<string, typeof filteredTimeSlots>);
    }, [filteredTimeSlots]);

    return (
        <div className='w-full flex flex-col justify-between  h-full'>
            {isPending ? <Loader className='animate-spin' /> : isError ? <div className="flex gap-2 items-center">
                <CircleAlert />
                <span>Error loading available timeslots</span>
            </div> : <div className='flex gap-10'>
                <div className='flex flex-col gap-3 w-[300px]'>
                    <Card className={cn('px-6 flex flex-row items-center cursor-pointer hover:border-green-700 transition-all', doctor === null && "border-green-600 border-2")} onClick={() => setDoctor(null)}>
                        <Avatar name={''} className='h-10 w-10' />
                        <span className='text-lg'>
                            All specialists
                        </span>
                    </Card>
                    {availableDoctors.map(d =>
                        <Card className={cn('px-6 flex flex-row items-center cursor-pointer hover:border-green-700 transition-all', doctor && doctor.doctor_id == d.doctor_id && "border-green-600 border-2")} onClick={() => setDoctor(d)}>
                            <Avatar name={`${d.first_name} ${d.last_name}`} bgColor={stringToColor(`${d.first_name} ${d.last_name}`)} className='h-10 w-10' />
                            <div className='flex flex-col'>
                                <span className='text-lg'>
                                    {d.first_name} {d.last_name}
                                </span>
                                <div className='flex gap-2 mt-0.5'>
                                    <Badge className='capitalize'>{d.specialization}</Badge> 
                                <Badge className='bg-green-900'>${d.amount}</Badge></div>
                            </div>
                        </Card>)}

                </div>
                <ScrollArea className='max-h-[600px] w-max flex-1'>
                    <div className='flex flex-col gap-4'>
                        {Object.entries(groupedTimeSlots).map(([dayLabel, slots]) => {
                            const date = new Date(slots[0].start); // zakładamy że wszystkie sloty w tej grupie mają ten sam dzień

                            return (
                                <div key={dayLabel} className="mb-6">
                                    <h3 className="text-xl font-semibold mb-2 flex items-center">
                                        <Calendar className='text-green-700 mr-2' /> {formatWeekDayName(date)}, {dayLabel}
                                    </h3>
                                    <div className="flex flex-wrap gap-2">
                                        {slots.map((slot) => {
                                            const start = new Date(slot.start);
                                            const end = new Date(slot.end);
                                            return (
                                                <Card key={slot.id} className={cn("px-4 py-2 text-sm flex flex-row items-center gap-2 cursor-pointer hover:border-green-700 transition-all", timeslot && timeslot.id === slot.id && "border-2 border-green-600")} onClick={() => setTimeslot(slot)}>
                                                    <Avatar name={`${slot.doctor.first_name} ${slot.doctor.last_name}`} bgColor={stringToColor(`${slot.doctor.first_name} ${slot.doctor.last_name}`)} className='h-6 w-6 text-xs' />
                                                    {formatTime(start)} - {formatTime(end)}
                                                </Card>
                                            );
                                        })}
                                    </div>
                                </div>
                            );
                        })}

                    </div>
                </ScrollArea>
            </div>}
            {timeslot && <Card className='p-4 mt-auto'>
                <Button className='ml-auto bg-emerald-600 hover:bg-emerald-700'>Go to payment</Button>
            </Card>
            }
        </div>
    )
}

export default BookAService;
