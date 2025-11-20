"use client";

import { useState } from 'react';
import { WorkflowInstructions } from './components/WorkflowInstructions';
import { WorkflowForm } from './components/WorkflowForm';
import { WorkflowFormData } from './types/workflow';

const Page = () => {

  const [formData, setFormData] = useState<WorkflowFormData>(
    {
      query:"",
      owner:"",
      repo:""
    }
  )
  const isLoading = false;
  
  return (
    <div>
      <h1>Hello World</h1>
      <div>
        <WorkflowInstructions />
      </div>
      <div>
        <WorkflowForm formData={formData} isLoading={isLoading}/>
      </div>
    </div>

  )
}

export default Page;