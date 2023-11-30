import React, { useState } from 'react';
import StarRating from './StarRating';

const RatingModal = ({ show, handleClose, itinerary_id }) => {
    const [rating, setRating] = useState(0);

    const handleRating = (rating) => {
        setRating(rating);
    }

    const saveRating = async () => {
        const response = await fetch(`http://localhost:8000/itineraries/${itinerary_id}/rating`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ rating: Math.round(rating) }),
        });

        if (!response.ok) {
            throw new Error('Failed to save rating');
        }
        handleClose();
    }



    return (
        <div className={`modal-container ${show ? 'modal-open' : ''}`}>
            <div className={`modal-backdrop fade ${show ? 'show' : ''}`}></div>
            <div class={`modal fade ${show ? 'show d-block' : ''}`} tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLabel">Rate the Itinerary</h5>
                            <button type="button" class="btn-close" data-mdb-ripple-init data-mdb-dismiss="modal" aria-label="Close" onClick={handleClose}></button>
                        </div>
                        <div class="modal-body">
                            <StarRating handleRating={handleRating} />
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-mdb-ripple-init data-mdb-dismiss="modal" onClick={handleClose}>Close</button>
                            <button type="button" class="btn btn-primary" data-mdb-ripple-init onClick={saveRating}>Save changes</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    );
}

export default RatingModal;