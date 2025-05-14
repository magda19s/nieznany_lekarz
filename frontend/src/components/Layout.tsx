import { Button } from "@/components/ui/button";
import logo from "@/assets/logo.png";
import shape1 from "@/assets/shape1.png";
import { Card } from "@/components/ui/card";
import { Outlet } from 'react-router-dom';
import { NavLink } from "react-router-dom";
function Layout() {
    const navLinkClass = ({ isActive }: { isActive: boolean }) =>
        isActive ? "text-green-600 font-semibold" : "text-gray-700 hover:text-green-500";

    return (
        <main className="h-screen bg-white flex flex-col">
            {/* Header */}
            <img src={shape1} alt="shape 1" className="fixed right-[-300px] top-[-220px] bottom-0 h-[190vh] -rotate-120" />
            <Card className="min-h-[88vh] max-h-[88vh] z-1 bg-white h-full border-none p-10 px-20 m-20 rounded-4xl shadow-2xl">
                <header className="flex justify-between items-center py-4 mb-10">
                    <div className="flex items-center gap-4">
                        <img src={logo} alt="Nieznany Lekarz Logo" className="h-16 w-16" />
                        <p className="text-3xl font-bold text-teal-700">
                            Nieznany Lekarz
                        </p>
                    </div>
                    <nav className="hidden md:flex space-x-6 text-xl">
                        <NavLink to="/" className={navLinkClass}>Home</NavLink>
                        <NavLink to="/about-us" className={navLinkClass}>About Us</NavLink>
                        <NavLink to="/services" className={navLinkClass}>Services</NavLink>
                        <NavLink to="/contact" className={navLinkClass}>Contact</NavLink>
                    </nav>
                    <Button className="bg-emerald-600 hover:bg-emerald-700 text-white text-xl px-6 py-3">Register Now</Button>
                </header>
                <Outlet />
            </Card>
        </main>
    )
}

export default Layout