'use client';
import CustomerForm from '../../../../components/forms/CustomerForm';


export default function EditCustomerPage({ params }: { params: { id: string } }) {
  return <CustomerForm id={params.id} />;
}
