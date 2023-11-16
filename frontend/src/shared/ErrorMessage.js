import React from 'react';


const ErrorMessage = ({ message }) => {
    return (
        <div className="alert alert-danger" role="alert">
            <p className='mb-0'>{message}</p>
        </div>
    );
};

export default ErrorMessage;
