import { motion } from "framer-motion";
import shape2 from "@/assets/shape2.png";
import doctors from "@/assets/team.png";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";

export default function AboutUs() {
  return (
    <div className="flex flex-row items-between">
      <motion.div
        initial={{ opacity: 0, x: -40 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6 }}
        className="max-w-xl space-y-6 my-auto"
      >
        <h2 className="text-4xl md:text-5xl font-bold text-gray-900 pb-8">
          Meet the <span className="text-emerald-600">Team Behind</span> the Care
        </h2>
        <p className="text-gray-600 text-xl pb-10">
          We're passionate about redefining healthcare access. Our mission is to connect patients with trusted medical professionals in the simplest way possible.
        </p>
        <Link to="/contact">
          <Button className="bg-emerald-600 hover:bg-emerald-700 text-white text-xl px-10 py-6">Contact Us</Button>
        </Link>
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
            alt="Our Team"
            className="z-1 h-full rounded-4xl shadow-lg"
          />
          <div className="absolute top-4 left-4 bg-white p-2 rounded-xl shadow text-sm text-green-700 font-medium">
            10+ Years of Experience
          </div>
          <div className="absolute bottom-4 right-4 bg-white p-2 rounded-xl shadow text-sm text-green-700">
            ✓ Dedicated Support<br />
            ✓ Trusted by thousands
          </div>
        </div>
      </motion.div>
    </div>
  );
}
