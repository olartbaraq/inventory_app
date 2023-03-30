import { FC } from "react";
import AuthComponent from "../components/AuthComponent";



const SignUp: FC = () => {
  return (
    <AuthComponent
    titleText="Verify User" 
    isPassword={false}
    buttonText="Verify"
    newUserText="Go Back"
    linkPath="/login"/>
  );
};

export default SignUp;