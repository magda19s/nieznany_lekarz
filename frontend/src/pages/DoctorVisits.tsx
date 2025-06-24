import { VisitsApi } from '@/api/VisitsApi';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { cn } from '@/lib/utils';
import type { Visit } from '@/types/Visit';
import { formatDate, formatTime } from '@/utils/formatter';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Loader, CircleAlert, Check, Plus } from 'lucide-react';
import { useEffect, useMemo, useState, type FC } from 'react'

const DoctorVisits: FC = () => {
    const [selectedVisit, setSelectedVisit] = useState<Visit | null>(null);
    const { data: visits = [], isPending, isError } = useQuery({
        queryKey: ["visits-doctor"],
        queryFn: VisitsApi.getDoctorVisits
    });
    const groupedVisits = useMemo(() => {
        const groups = {
            paid: {} as Record<string, typeof visits>,
            unpaid: {} as Record<string, typeof visits>
        };

        for (const visit of visits) {
            const dateKey = formatDate(new Date(visit.time_slot.start));
            const statusGroup = visit.status === "paid" ? "paid" : "unpaid";

            if (!groups[statusGroup][dateKey]) {
                groups[statusGroup][dateKey] = [];
            }
            groups[statusGroup][dateKey].push(visit);
        }

        return groups;
    }, [visits]);

    const toggleVisit = (visit: Visit) => {
        if (!selectedVisit || selectedVisit.id !== visit.id) {
            setSelectedVisit(visit);
        } else {
            setSelectedVisit(null);
        }
    }

    return (
        <div className='w-full flex flex-col justify-between h-full'>
            {isPending ? <Loader className='animate-spin' /> : isError ? <div className="flex gap-2 items-center">
                <CircleAlert />
                <span>Error loading visits</span>
            </div> :
                <ScrollArea className='h-[800px]'>
                    <div className='w-full flex flex-row justify-between gap-10'>
                        <div className='flex-grow max-w-1/2'>
                            {["paid", "unpaid"].map(statusGroup => (
                                <div key={statusGroup} className="mb-10">
                                    <h2 className="text-2xl font-bold capitalize mb-4">
                                        {statusGroup === "unpaid" ? "Unpaid Visits" : "Paid Visits"}
                                    </h2>
                                    {Object.entries(groupedVisits[statusGroup]).map(([dayLabel, dailyVisits]) => {
                                        const date = new Date(dailyVisits[0].time_slot.start);

                                        return (
                                            <div key={dayLabel} className="mb-6">
                                                <h3 className="text-xl font-semibold mb-2">{formatDate(date)}</h3>
                                                <div className="flex flex-wrap gap-2">
                                                    {dailyVisits.map((v) => {
                                                        const visit = v as Visit;
                                                        const start = new Date(visit.time_slot.start);
                                                        const end = new Date(visit.time_slot.end);
                                                        return (
                                                            <Card key={visit.id} className={cn("px-4 py-2 text-sm flex flex-col gap-1 w-[220px] hover:border-green-600 hover:shadow-md transition-all", selectedVisit?.id === v.id && "bg-muted")} onClick={() => toggleVisit(v)}>
                                                                <div><strong>Time:</strong> {formatTime(start)} - {formatTime(end)}</div>
                                                                <div><strong>Patient ID:</strong> {visit.patient_id}</div>
                                                                <div><strong>Status:</strong> {visit.status}</div>
                                                                {visit.status === "paid" && <div>{visit.notes ? <Badge className='bg-green-700 ml-auto'><Check /> Notes added</Badge> : <Badge><Plus /> Add notes</Badge>}</div>}
                                                            </Card>
                                                        );
                                                    })}
                                                </div>
                                            </div>
                                        );
                                    })}
                                </div>
                            ))}
                        </div>
                        {selectedVisit && <div className='h-[800px] w-[1px] bg-foreground text-transparent'>.</div>}
                        {selectedVisit && <VisitDetails visit={selectedVisit} />}
                    </div>
                </ScrollArea>
            }
        </div>
    )
}

export default DoctorVisits


const VisitDetails: FC<{ visit: Visit }> = ({ visit }) => {
    const queryClient = useQueryClient();
    const [note, setNote] = useState("");

    useEffect(() => {
        setNote(visit.notes ?? "")
    }, [visit]);

    const { data: patient, isPending, isError } = useQuery({
        queryFn: () => VisitsApi.getPatient(visit.patient_id),
        queryKey: ["patient", { patient_id: visit.patient_id }]
    })

    const { mutate: updateNote, isPending: isSaving } = useMutation({
        mutationFn: (newNote: string) =>
            VisitsApi.addVisitNote(visit.id, newNote),
        onSuccess: (updatedVisit) => {
            queryClient.setQueryData(["visits-doctor"], (oldData: Visit[] | undefined) => {
                if (!oldData) return [];

                return oldData.map(visit =>
                    visit.id === updatedVisit.id ? updatedVisit : visit
                );
            });
        },
        onError: () => {
            alert("Failed to save note.");
        }
    });

    const handleSaveNote = async () => {
        await updateNote(note);
    };

    return <Card className='min-h-[600px] flex-grow max-w-1/2 p-6 flex flex-col gap-4 mr-5'>
        <h2 className="text-2xl font-semibold">Visit Details</h2>
        {isPending ? <Loader className='animate-spin' /> : isError ? <div className="flex gap-2 items-center">
            <CircleAlert />
            <span>Error loading visit details</span>
        </div> : <><div>
            <p><strong>Patient:</strong> {patient.first_name} {patient.last_name} ({patient.email})</p>
            <p><strong>Date:</strong> {formatDate(new Date(visit.time_slot.start))}</p>
            <p><strong>Time:</strong> {formatTime(new Date(visit.time_slot.start))} - {formatTime(new Date(visit.time_slot.end))}</p>
            <p><strong>Status:</strong> {visit.status}</p>
            <p><strong>Price:</strong> ${visit.doctor.amount}</p>
        </div>
            {
                visit.status === "paid" && <div className="flex flex-col gap-2 mt-4">
                    <label htmlFor="notes" className="font-medium">Add notes for the patient</label>
                    <textarea
                        id="notes"
                        rows={5}
                        className="border rounded-md p-2 w-full"
                        value={note}
                        onChange={(e) => setNote(e.target.value)}
                        placeholder="Add or edit your notes..."
                    />
                    <Button className="self-start bg-green-700 hover:bg-green-800 ml-auto w-[100px]" onClick={() => void handleSaveNote()} disabled={isSaving}>
                        {isSaving ? <Loader className="animate-spin w-4 h-4" /> : "Save Note"}
                    </Button>
                </div>
            }</>}
    </Card>
};
