import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import shape2 from "@/assets/shape2.png";
import doctors from "@/assets/doctors.png";

export default function HomePage() {
  return (
    <div className="flex flex-row items-between">
      <motion.div
        initial={{ opacity: 0, x: -40 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6 }}
        className="max-w-xl space-y-6 my-auto"
      >
        <h2 className="text-4xl md:text-5xl font-bold text-gray-900 pb-8">
          Get Quick <span className="text-emerald-600">Medical Services</span>
        </h2>
        <p className="text-gray-600 text-xl pb-10">
          Access healthcare faster than ever. Our platform connects you with expert doctors and clinics with just a few clicks.
        </p>
        <Button className="bg-emerald-600 hover:bg-emerald-700 text-white text-xl px-10 py-6">Book a service</Button>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, x: 40 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6 }}
        className="w-full max-w-md mb-12 md:mb-0 ml-auto mr-10"
      >
        <div className="relative">
          <img src={shape2} alt="shape-2" className="absolute top-20 right-10 scale-160 scale-x-180 -z-1" />
          <img
            src={doctors}
            alt="Doctors"
            className="z-1 h-full rounded-4xl shadow-lg"
          />
          <div className="absolute top-4 left-4 bg-white p-2 rounded shadow text-sm text-green-700 font-medium">
            1520+ Active Clients
          </div>
          <div className="absolute bottom-4 right-4 bg-white p-2 rounded shadow text-sm text-green-700">
            ✓ 20% off for new users<br />
            ✓ Expert Doctors
          </div>
        </div>
      </motion.div>
    </div>
  );
}