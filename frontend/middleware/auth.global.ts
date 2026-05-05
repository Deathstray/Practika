import { useAuthStore } from "~/stores/auth";

export default defineNuxtRouteMiddleware((to) => {
  const auth = useAuthStore();
  auth.restore();

  if (to.path === "/login" || to.path === "/register") return;

  if (!auth.isLoggedIn) return navigateTo("/login");

  const role = auth.role;
  if (to.path.startsWith("/dispatcher") && role !== "dispatcher")
    return navigateTo(`/${role}`);
  if (to.path.startsWith("/employee") && role !== "employee")
    return navigateTo(`/${role}`);
  if (to.path.startsWith("/driver") && role !== "driver")
    return navigateTo(`/${role}`);
});
