export interface ContainerType {
  id: string;
  work_id: string;
  work_container: string;
  connection_id?: string;
  vnc_url?: string;
}

export interface RequestBody {
  id: string;
  work_id: string;
  work_container: string;
  username: string;
  password: string;
  connection_id?: string;
}