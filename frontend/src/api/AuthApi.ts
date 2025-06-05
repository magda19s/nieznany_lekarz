import { type User, type UserCreated } from "@/types/User";
import axios from "axios";

const AxiosAuthApi = axios.create({
  baseURL: import.meta.env.VITE_AUTH_API_URL,
  timeout: 4800,
});


class AuthApi {
  static async logIn(credential: string) {
    const { data: info } = await AxiosAuthApi.post<UserCreated>("/auth/google", { credential });
    return info;
  }
  
  static async getInfo(user_id: string) {
    const { data: user } = await AxiosAuthApi.get<User>(`/auth/user/${user_id}`);
    return user;
  }
}

export { AxiosAuthApi, AuthApi };