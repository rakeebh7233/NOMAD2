import React, { useState } from 'react';
import { FaStar } from 'react-icons/fa';

const StarRating = ({ handleRating }) => {
    const [rating, setRating] = useState(0);
    const [hover, setHover] = useState(0);
    
    return (
        <div>
            {[...Array(5)].map((star, i) => {
                const ratingValue = i + 1;

                return (
                    <label>
                        <input 
                            type="radio" 
                            name="rating" 
                            value={ratingValue} 
                            onClick={() => {
                                setRating(ratingValue); 
                                handleRating(Number(ratingValue));
                            }}
                        />
                        <FaStar 
                            className="star" 
                            color={ratingValue <= (hover || rating) ? "#ffc107" : "#e4e5e9"} 
                            size={40} 
                            onMouseEnter={() => setHover(ratingValue)}
                            onMouseLeave={() => setHover(null)} />
                    </label>
                );
            })}
        </div>
    );
}

export default StarRating;