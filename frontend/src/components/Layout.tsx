import logo from "@/assets/logo.png";
import shape1 from "@/assets/shape1.png";
import { Card } from "@/components/ui/card";
import { Outlet, NavLink } from "react-router-dom";
import { GoogleLogin, googleLogout } from "@react-oauth/google";
import { useEffect, useState } from "react";
import { jwtDecode, type JwtPayload } from "jwt-decode";
import { AxiosAuthApi, AuthApi } from "@/api/AuthApi";
import { AxiosPaymentsApi } from "@/api/PaymentsApi";
import { AxiosVisitsApi } from "@/api/VisitsApi";
import { useMutation, useQuery } from "@tanstack/react-query";
import { roleState } from "@/state/role";
import { tokenState } from "@/state/token";
import type { User } from "@/types/User";
import { CircleAlert, Loader, LogOut, User as UserIcon } from "lucide-react";
import { useAtom } from "jotai";
import { Button } from "./ui/button";
import axios from "axios";

function Layout() {
    const navLinkClass = ({ isActive }: { isActive: boolean }) =>
        isActive ? "text-green-600 font-semibold" : "text-gray-700 hover:text-green-500";
    const [role, setRole] = useAtom(roleState);
    const [token, setToken] = useAtom(tokenState);
    const [user, setUser] = useState<User | null>(null);

    const decoded = token ? jwtDecode<JwtPayload>(token) : null;
    const userId = decoded?.user_id;
    console.log("role: ", role)

    const { mutate: logIn, isPending: isLoginPending } = useMutation({
        mutationFn: (credentials: string) => AuthApi.logIn(credentials),
        onError: (e) => {
            console.log("error", e)
        },
        onSuccess: (data) => {
            setToken(data.access_token);
            setRole(data.user.role);
            setUser(data.user);
            localStorage.setItem("token", data.access_token);
            localStorage.setItem("refresh", data.refresh); // ✅ zapisz refresh
        },
    });

    const { data: dataUser, isPending } = useQuery({
        queryKey: ["user", userId],
        queryFn: () => AuthApi.getInfo(userId),
        enabled: !!token && !!userId,
        refetchOnMount: false,
        refetchOnWindowFocus: false
    });

    useEffect(() => {
        if (dataUser) {
            setRole(dataUser.role)
            setUser(dataUser);
        }
    }, [dataUser, setRole]);

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

    useEffect(() => {
        const refreshToken = async (refresh: string) => {
            try {
                const res = await axios.post("/auth/token/refresh/", { refresh });
                const newAccessToken = res.data.access;
                setToken(newAccessToken);
                localStorage.setItem("token", newAccessToken);
                return newAccessToken;
            } catch (error) {
                console.error("Token refresh failed", error);
                googleLogout();
                setToken(null);
                setRole("guest");
                localStorage.removeItem("token");
                localStorage.removeItem("refresh");
                localStorage.removeItem("role");
                return null;
            }
        };

        const storageToken = localStorage.getItem("token");
        const refresh = localStorage.getItem("refresh");

        if (storageToken) {
            const decodedToken = jwtDecode(storageToken);
            const currentTime = Date.now() / 1000;
            if (decodedToken.exp && decodedToken.exp < currentTime) {
                if (refresh) {
                    void refreshToken(refresh).then((newToken) => {
                        if (newToken) {
                            void logIn(newToken);
                        }
                    });
                } else {
                    googleLogout();
                    setToken(null);
                    setRole("guest");
                    localStorage.removeItem("token");
                    localStorage.removeItem("refresh");
                }
            } else {
                setToken(storageToken);
            }
        }
    }, [logIn, setRole, setToken]);

    return (
        <main className="h-screen bg-white flex flex-col">
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
                        {["pacjent", "patient"].includes(role) && <NavLink to="/new-service" className={navLinkClass}>Book a service</NavLink>}
                        {["lekarz", "doctor"].includes(role) && <NavLink to="/my-services" className={navLinkClass}>My visits</NavLink>}
                        {["lekarz", "doctor"].includes(role) && <NavLink to="/my-patients" className={navLinkClass}>My patients</NavLink>}
                        <NavLink to="/contact" className={navLinkClass}>Contact</NavLink>
                    </nav>
                    <div className="flex gap-10">
                        {
                            !token ? <GoogleLogin onSuccess={(credentialResponse) => {
                                void logIn(credentialResponse.credential as string)
                            }} /> :
                                (isPending || isLoginPending) ? <Loader className="animate-spin" /> : user ? (
                                    <div className="flex gap-2 items-center px-2 py-1 rounded-2xl border-emerald-500 border-2 ">
                                        <UserIcon />
                                        <span>{user.first_name} {user.last_name}</span>
                                    </div>
                                ) : (
                                    <div className="flex gap-2 items-center">
                                        <CircleAlert />
                                        <span>Error logging in</span>
                                    </div>
                                )
                        }
                        {token && <Button size="icon" onClick={() => {
                            googleLogout();
                            setToken(null);
                            setRole("guest");
                            localStorage.clear();
                        }}><LogOut /></Button>}
                    </div>
                </header>
                <Outlet />
            </Card>
        </main>
    );
}

export default Layout;
