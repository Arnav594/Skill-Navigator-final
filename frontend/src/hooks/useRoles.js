import { useState, useEffect } from "react";
import { fetchRoles } from "../api/client";

export function useRoles() {
  const [roles, setRoles] = useState([]);
  const [selectedRole, setSelectedRole] = useState("");
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchRoles()
      .then((data) => {
        setRoles(data);
        if (data.length > 0) setSelectedRole(data[0]);
      })
      .catch(() =>
        setError("Could not connect to backend. Please make sure the server is running.")
      );
  }, []);

  return { roles, selectedRole, setSelectedRole, error };
}
