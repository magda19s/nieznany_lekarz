import logo from "@/assets/logo.png";
import shape1 from "@/assets/shape1.png";
import { Card } from "@/components/ui/card";
import { Outlet } from 'react-router-dom';
import { NavLink } from "react-router-dom";
import { GoogleLogin, googleLogout } from "@react-oauth/google";
import { useEffect, useState } from "react";
import { jwtDecode } from "jwt-decode";
import { AxiosAuthApi, AuthApi } from "@/api/AuthApi";
import { AxiosPaymentsApi } from "@/api/PaymentsApi";
import { AxiosVisitsApi } from "@/api/VisitsApi";
import { useMutation } from "@tanstack/react-query";
import { roleState } from "@/state/role";
import { tokenState } from "@/state/token";
import type { User, UserRole } from "@/types/User";
import { CircleAlert, Loader, LogOut, User as UserIcon } from "lucide-react";
import { useAtom } from "jotai";
import { Button } from "./ui/button";

function Layout() {
    const navLinkClass = ({ isActive }: { isActive: boolean }) =>
        isActive ? "text-green-600 font-semibold" : "text-gray-700 hover:text-green-500";
    const [role, setRole] = useAtom(roleState);
    const [token, setToken] = useAtom(tokenState);
    const [user, setUser] = useState<User | null>(null);

    useEffect(() => {
        const token = localStorage.getItem("token");
        const role = localStorage.getItem("role");
        if (token) {
            const decodedToken = jwtDecode(token as string);
            const currentTime = Date.now() / 1000;
            if (decodedToken.exp && decodedToken.exp < currentTime) {
                localStorage.removeItem("token");
                setToken(null);
                setRole("guest");
                googleLogout();
            } else {
                setToken(token as string);
                setRole(role ? role as UserRole : "guest")
            }
        }
    }, [setRole, setToken]);

    const { mutate: getUser, isPending } = useMutation({
        mutationFn: (credentials: string) => AuthApi.getInfo(credentials),
        onError: (e) => {
            console.log("error", e)
        },
        onSuccess: (data) => {
            setToken(data.access_token);
            setRole(data.user.role);
            localStorage.setItem("token", data.access_token);
            localStorage.setItem("role", data.user.role);
            console.log(data);
            setUser(data.user);
        },
    });

    useEffect(() => {
        const authInterceptor = AxiosAuthApi.interceptors.request.use(config => {
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
            return config;
        });

        const paymentsInterceptor = AxiosPaymentsApi.interceptors.request.use(config => {
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
            return config;
        });

        const visitsInterceptor = AxiosVisitsApi.interceptors.request.use(config => {
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
            return config;
        });

        return () => {
            AxiosAuthApi.interceptors.request.eject(authInterceptor);
            AxiosPaymentsApi.interceptors.request.eject(paymentsInterceptor);
            AxiosVisitsApi.interceptors.request.eject(visitsInterceptor);
        };
    }, [token]);

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
                        {role === "pacjent" && <NavLink to="/services" className={navLinkClass}>Umów wizytę</NavLink>}
                        {role === "lekarz" && <NavLink to="/services" className={navLinkClass}>Moje wizyty</NavLink>}
                        {role === "lekarz" && <NavLink to="/services" className={navLinkClass}>Moi pacjenci</NavLink>}
                        <NavLink to="/contact" className={navLinkClass}>Contact</NavLink>
                    </nav>
                    <div className="flex gap-10">
                        {
                            !token ? <GoogleLogin onSuccess={(credentialResponse) => {
                                void getUser(credentialResponse.credential as string)
                            }} /> :
                                isPending ? <Loader className="animate-spin" /> : user ?
                                    <div className="flex gap-2 items-center px-2 py-1 rounded-2xl border-emerald-500 border-2 ">
                                        <UserIcon />
                                        <span>{user.first_name} {user.last_name}</span>
                                    </div>
                                    :
                                    <div className="flex gap-2 items-center">
                                        <CircleAlert />
                                        <span>Błąd logowania</span>
                                    </div>
                        }
                        {token && <Button size="icon" onClick={() => {
                            googleLogout();
                            setToken(null);
                            setRole("guest");
                        }}
                        ><LogOut /></Button>}
                    </div>
                </header>
                <Outlet />
            </Card>
        </main>
    )
}

export default Layout