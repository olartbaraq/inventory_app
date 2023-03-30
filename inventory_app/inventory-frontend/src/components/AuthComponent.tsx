import { FC } from "react"
import { Form, Input, Button } from "antd";
import { Link } from "react-router-dom";
import '../BackgroundVideo.css'
import '../style.css'

interface AuthComponentProps {
    titleText?: string,
    isPassword?: boolean,
    buttonText?: string,
    newUserText?: string,
    linkPath?: string
}


const AuthComponent:FC<AuthComponentProps> = ({
    titleText,
    isPassword=true,
    buttonText,
    newUserText,
    linkPath="/verify"
}) => {
    return <div>
        <video loop autoPlay muted className="bg-video">
            <source src={require('../assets/inventory.mp4')} type="video/mp4" />
        </video>
    <div className="login">
        <div className="inner">
            <div className="header">
            <h3>{titleText}</h3>
            <h2>Inventory</h2>
            </div>

            <Form
                layout="vertical"
                >
                <Form.Item label="Email">
                    <Input placeholder="Email" type="email"/>
                </Form.Item>
                {isPassword && 
                <Form.Item label="Password">
                    <Input placeholder="Password" type="password"/>
                </Form.Item> }
                <Form.Item>
                    <Button type="primary" block>{buttonText}</Button>
                </Form.Item>
            </Form>
            <div className="link">
                <Link to={linkPath}>{newUserText}
                </Link>
            </div>
        </div>
    </div>
    </div>
}

export default AuthComponent