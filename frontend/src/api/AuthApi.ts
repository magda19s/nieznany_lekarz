import type { UserCreated } from "@/types/User";
import axios from "axios";

const AxiosAuthApi = axios.create({
  baseURL: import.meta.env.VITE_AUTH_API_URL,
  timeout: 4800,
});


class AuthApi {
    static async getInfo(credential: string) {
        const { data: info } = await AxiosAuthApi.post<UserCreated>("/auth/google", { credential });
        return info;
    } 
}

export {AxiosAuthApi, AuthApi};