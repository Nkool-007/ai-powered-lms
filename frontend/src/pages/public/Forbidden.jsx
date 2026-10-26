import { Link } from "react-router-dom";
export default function Forbidden(){return <div className="container py-5 text-center"><div className="display-1 fw-bold">403</div><h1>Access Denied</h1><p className="text-secondary">You do not have permission to access this page.</p><Link to="/" className="btn btn-primary">Go Home</Link></div>;}
