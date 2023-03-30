import { FC } from "react";
import AuthComponent from "../components/AuthComponent";



const Login: FC = () => {
  return (
    <AuthComponent
    titleText="Sign In" 
    buttonText="Login"
    newUserText="New User ?" 
    linkPath="/verify"/>

  );
};

export default Login;
