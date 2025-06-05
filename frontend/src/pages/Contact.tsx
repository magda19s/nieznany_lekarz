import { motion } from "framer-motion";
import shape2 from "@/assets/shape2.png";
import contactImg from "@/assets/contact.jpg"; // Add a relevant image to /assets
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";

export default function Contact() {
  return (
    <div className="flex flex-row items-between">
      <motion.div
        initial={{ opacity: 0, x: -40 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6 }}
        className="max-w-xl space-y-6 my-auto"
      >
        <h2 className="text-4xl md:text-5xl font-bold text-gray-900 pb-8">
          Get in <span className="text-emerald-600">Touch With Us</span>
        </h2>
        <p className="text-gray-600 text-xl pb-10">
          Questions? Feedback? Need help? We’re here for you. Reach out and we’ll get back to you as soon as possible.
        </p>

        <div className="space-y-4 text-lg text-gray-700">
          <p><strong>Email:</strong> support@nieznanylekarz.pl</p>
          <p><strong>Phone:</strong> +48 123 456 789</p>
          <p><strong>Address:</strong> ul. Zdrowia 10, 00-001 Warszawa</p>
        </div>

        <Link to="">
          <Button className="mt-6 bg-emerald-600 hover:bg-emerald-700 text-white text-xl px-10 py-6">
            Send a Message
          </Button>
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
            src={contactImg}
            alt="Contact illustration"
            className="z-1 h-full rounded-4xl shadow-lg"
          />
          <div className="absolute top-4 left-4 bg-white p-2 rounded-xl shadow text-sm text-green-700 font-medium">
            Response in under 24h
          </div>
          <div className="absolute bottom-4 right-4 bg-white p-2 rounded-xl shadow text-sm text-green-700">
            ✓ Friendly support<br />
            ✓ Multilingual service
          </div>
        </div>
      </motion.div>
    </div>
  );
}
