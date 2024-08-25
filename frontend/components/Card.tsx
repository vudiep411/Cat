import { useChatStore } from '@/store/store';
import React, { useState } from 'react'
import { FaStar } from 'react-icons/fa';
import { AiFillEdit } from "react-icons/ai";

interface Cat {
  adaptability: number;
  affection_level: number;
  breed_name: string;
  child_friendly: number;
  description: string;
  dog_friendly: number;
  energy_level: number;
  grooming: number;
  id: string;
  image_url: string;
  indoor: number;
  intelligence: number;
  life_span: string;
  origin: string;
  social_needs: number;
  stranger_friendly: number;
  temperament: string;
  weight: string;
  favorite: boolean;
}

interface CatCardProps {
  cat: Cat;
}
const Card: React.FC<CatCardProps> = ({ cat }) => {
  const addOrRemoveFavorite = useChatStore((state: any) => state.addOrRemoveFavorite);
  const activeTab = useChatStore((state: any) => state.activeTab)
  const editPreference = useChatStore((state: any) => state.editPreference)
  const [isEditing, setIsEditing] = useState(false);
  const [breedName, setBreedName] = useState(cat.breed_name);
  const [description, setDescription] = useState(cat.description);
  const handleSave = () => {
    setIsEditing(false)
    console.log(cat.id, breedName, description)
    cat.description = description
    cat.breed_name = breedName
    editPreference(cat.id, description, breedName)
  }

  return (
    <div className="rounded-xl shadow-xl border">
      <div className='relative mx-auto rounded overflow-hidden'>
        <img src={cat.image_url} alt={cat.breed_name} className="w-full h-64 object-scale-down mt-2" />
        <div 
          onClick={() => addOrRemoveFavorite(cat.id, cat.favorite, {
            description: cat.description,
            image_id: cat.id, 
            name: cat.breed_name
          })}
          className="absolute top-1 right-1 lg:top-3 lg:right-3 cursor-pointer"
        >
          <FaStar color={cat.favorite ? 'gold' : 'lightgray'} size={24} />
        </div>
      </div>
      <hr className='mt-2'/>
      <div className="p-4">
      {isEditing ? (
          <div>
            <input
              type="text"
              value={breedName}
              onChange={(e) => setBreedName(e.target.value)}
              className="text-xl font-bold mb-2 w-full border border-gray-300 rounded p-2"
            />
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full mb-2 border border-gray-300 rounded p-2"
            />
            <button onClick={handleSave} className="mr-2 px-3 py-1 bg-blue-500 text-white rounded-md">
              Save
            </button>
            <button onClick={() => setIsEditing(false)} className="px-3 py-1 bg-gray-500 text-white rounded-md">
              Cancel
            </button>
          </div>
        ) : (
          <div>
            <div className='flex'> 
              <h2 className="text-xl font-bold">{cat.breed_name}</h2>
              { activeTab === 'Favorites' && <button onClick={() => setIsEditing(true)} className="ml-auto text-sm hover:scale-105"><AiFillEdit size={24}/></button> }
            </div>
            <br/>
            <p >{cat.description}</p>
          </div>
        )}
        <ul className="mt-2 space-y-1">
          <li><strong>Origin:</strong> {cat.origin}</li>
          <li><strong>Life Span:</strong> {cat.life_span}</li>
          <li><strong>Weight:</strong> {cat.weight}</li>
          <li><strong>Adaptability:</strong> {cat.adaptability}</li>
          <li><strong>Affection Level:</strong> {cat.affection_level}</li>
          <li><strong>Child Friendly:</strong> {cat.child_friendly}</li>
          <li><strong>Dog Friendly:</strong> {cat.dog_friendly}</li>
          <li><strong>Energy Level:</strong> {cat.energy_level}</li>
          <li><strong>Grooming:</strong> {cat.grooming}</li>
          <li><strong>Intelligence:</strong> {cat.intelligence}</li>
          <li><strong>Social Needs:</strong> {cat.social_needs}</li>
          <li><strong>Stranger Friendly:</strong> {cat.stranger_friendly}</li>
          <li><strong>Temperament:</strong> {cat.temperament}</li>
        </ul>
      </div>
    </div>
  );
}

export default Card